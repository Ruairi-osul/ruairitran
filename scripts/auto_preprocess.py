import argparse
import os
import json
from functools import partial
from glob import glob
from continuous_dat import main as pack_to_dat
from autokilosort import main as ks


class Recording:

    def __init__(self, name, pre, cond):
        self.name = name
        self.pre = pre
        self.cond = cond

    def has_cond(self):
        return bool(self.cond)


def _get_options():
    parser = argparse.ArgumentParser(
        description='''primary preprocessing script.

        Finds files, calls pack to dat on associated sessions,
        concatenates those associated sessions.

        Finishes by running autokilosort
        ''')

    parser.add_argument('-e', '--experiment', required=True,
                        help='''experiment name.

                        this will change the method used to calculate
                        which files process

                        FOR GAT_DREADD:   'gd'
                        FOR SERT_DREADD:  'sd'
                        FOR CIT_WAY:      'cw'

                        ''')
    parser.add_argument('-c', '--config_file', required=True,
                        help='''path to preprocessing config file

        ''')
    parser.add_argument('-v', '--verbose', required=False, default=True)
    return parser.parse_args()


def get_subfolders(parent, containing_filetype=None, verbose=True):

    def _walklevel(some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    def _has_ext(path, ext):
        if '.' not in ext:
            ext = ''.join(['.', ext])
        return bool(glob(os.path.join(path, ''.join(['*', ext]))))

    try:
        paths = [x[0]
                 for x in _walklevel(parent, level=1) if os.path.isdir(x[0])]
        if parent in paths:
            del paths[paths.index(parent)]
    except AssertionError:
        if verbose:
            print('Could not find {} dir'.format(parent))
        raise

    if containing_filetype:
        f = partial(_has_ext, ext=containing_filetype)
        paths = list(filter(f, paths))

    return paths


def organise_into_objects(todo):
    out = []
    bases = list(map(os.path.basename, todo))
    recordings = set(['_'.join(x.split('_')[:-2]) for x in bases])
    for recording in recordings:
        try:
            pre = list(
                filter(lambda x: recording in x and 'pre' in x.lower(), todo))[0]
            pre = os.path.basename(pre)
        except IndexError:
            print('No pre file found for recording: {}'.format(recording))
            raise
        try:
            cond = list(
                filter(lambda x: recording in x and 'cno' in x.lower(), todo))[0]
            cond = os.path.basename(cond)
        except IndexError:
            print('No condition file found for recording {}. Continuing anyway'.format(
                recording))
            cond = None

        out.append(Recording(name=recording, pre=pre, cond=cond))
    return out


def cat_recordings(out_name, pre_file, cond_file, dat_file_dir):
    out_name = os.path.join(dat_file_dir, out_name, out_name) + '.dat'
    call_string = ' '.join([pre_file, cond_file])
    call_string = ' '.join(['cat', call_string, '>', out_name])
    if not os.path.exists(os.path.dirname(out_name)):
        os.mkdir(os.path.dirname(out_name))

    print('''Calling:\n\n{}\n\n

        '''.format(call_string))
    resp = os.system(call_string)
    if resp:
        print('Response from shell:\n\n'.format(resp))

    print('=' * 30)


def mv_recordings(out_name, pre_file, dat_file_dir):
    out_name = os.path.join(dat_file_dir, out_name, out_name) + '.dat'
    if not os.path.exists(os.path.dirname(out_name)):
        os.mkdir(os.path.dirname(out_name))

    call_string = ' '.join(['mv', pre_file, '>', out_name])

    print('''Calling:\n\n{}\n\n

        '''.format(call_string))
    resp = os.system(call_string)
    if resp:
        print('Response from shell:\n\n'.format(resp))

    print('=' * 30)


def get_files_todo(dat_file_dir, continuous_dir, verbose):

    try:
        done_files = get_subfolders(parent=dat_file_dir,
                                    containing_filetype='.dat',
                                    verbose=verbose)
    except AssertionError:  # triggers when cat dat file dir not found
        if verbose:
            print('''Could not find dat file directory
                Creating new directory {}'''.format(dat_file_dir))
        os.mkdir(dat_file_dir)
        done_files = []

    continuous_dirs = get_subfolders(parent=continuous_dir,
                                     containing_filetype='.continuous',
                                     verbose=verbose)

    dat_base = list(map(os.path.basename, done_files))

    if not dat_base:
        todo = continuous_dirs
    else:
        for path in dat_base:
            todo = list(filter(lambda x: path not in x,
                               continuous_dirs))
    return todo


def main(continuous_dir, dat_file_dir, temp_dat_dir,
         chan_map, reference_method,
         master_kilosort, config_kilosort, verbose, experiment):

    files_todo = get_files_todo(dat_file_dir,
                                continuous_dir, verbose)
    recordings = organise_into_objects(files_todo)

    for recording in recordings:
        if verbose:
            print('\n' * 20)
            print('Recording: {}'.format(recording.name))
            print('packing: {}'.format(recording.pre))
            print('cno file: {}'.format(recording.cond))
            print('\n' * 10)
        temp_pre = pack_to_dat(in_dir=continuous_dir,
                               recording=recording.pre,
                               out_dir=temp_dat_dir,
                               chan_map=chan_map)
        print('\n' * 5)
        print('Done')
        if recording.has_cond():
            print('\n' * 5)
            print('packing: {}'.format(recording.cond))
            print('\n' * 5)
            temp_cond = pack_to_dat(in_dir=continuous_dir,
                                    recording=recording.cond,
                                    out_dir=temp_dat_dir,
                                    chan_map=chan_map)
            print('\nAttempting to concatenate files')
            cat_recordings(out_name=recording.name,
                           pre_file=temp_pre,
                           cond_file=temp_cond,
                           dat_file_dir=dat_file_dir)
        else:
            print('\n' * 5)
            print('moving to dat folder: {}'.format(temp_pre))
            print('\n' * 5)
            mv_recordings(out_name=recording.name,
                          pre_file=temp_pre,
                          dat_file_dir=dat_file_dir)
    ks(master=master_kilosort,
        config=config_kilosort,
        parent=dat_file_dir)


if __name__ == '__main__':
    def _update_options_from_json(config_file):
        with open(config_file) as file:
            config_options = json.loads(file.read())
        return config_options

    def _extend_dirs(home_dir):
        '''given an exp home dir, return continuous and temp dirs

        returns: continuous_dir, temp_dat_dir, cat_dat_dir'''
        return (os.path.join(home_dir, 'continuous'),
                os.path.join(home_dir, 'temp_dat_dir'),
                os.path.join(home_dir, 'dat_files'))

    # converting to a dict so that it can be updated with config json
    args = vars(_get_options())
    args.update(_update_options_from_json(args['config_file']))
    args['continuous_dir'], args['temp_dat_dir'], args['dat_file_dir'] = _extend_dirs(
        args['exp_home_dir'])

    if args['experiment'] != 'gd':
        raise ValueError('''Automated preprocessing only implimented for GAT_DREADD
            at this time''')

    main(continuous_dir=args['continuous_dir'],
         dat_file_dir=args['dat_file_dir'],
         temp_dat_dir=args['temp_dat_dir'],
         chan_map=args['chan_map'],
         reference_method=args['reference_method'],
         master_kilosort=args['master_kilosort'],
         config_kilosort=args['config_kilosort'],
         verbose=args['verbose'],
         experiment=args['experiment'])
